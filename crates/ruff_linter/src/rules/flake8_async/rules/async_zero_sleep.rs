use ruff_diagnostics::Applicability;
use ruff_macros::{ViolationMetadata, derive_message_formats};
use ruff_python_ast::{self as ast, Expr, ExprCall, Int, Number};
use ruff_python_semantic::Modules;
use ruff_text_size::Ranged;

use crate::checkers::ast::Checker;
use crate::importer::ImportRequest;
use crate::rules::flake8_async::helpers::AsyncModule;
use crate::{AlwaysFixableViolation, Edit, Fix};

/// ## What it does
/// Checks for uses of `trio.sleep(0)` or `anyio.sleep(0)`.
///
/// ## Why is this bad?
/// `trio.sleep(0)` is equivalent to calling `trio.lowlevel.checkpoint()`.
/// However, the latter better conveys the intent of the code.
///
/// ## Example
/// ```python
/// import trio
///
///
/// async def func():
///     await trio.sleep(0)
/// ```
///
/// Use instead:
/// ```python
/// import trio
///
///
/// async def func():
///     await trio.lowlevel.checkpoint()
/// ```
/// ## Fix safety
/// This rule's fix is marked as unsafe if there's comments in the
/// `trio.sleep(0)` expression, as comments may be removed.
///
/// For example, the fix would be marked as unsafe in the following case:
/// ```python
/// import trio
///
///
/// async def func():
///     await trio.sleep(  # comment
///         # comment
///         0
///     )
/// ```
#[derive(ViolationMetadata)]
pub(crate) struct AsyncZeroSleep {
    module: AsyncModule,
}

impl AlwaysFixableViolation for AsyncZeroSleep {
    #[derive_message_formats]
    fn message(&self) -> String {
        let Self { module } = self;
        format!("Use `{module}.lowlevel.checkpoint()` instead of `{module}.sleep(0)`")
    }

    fn fix_title(&self) -> String {
        let Self { module } = self;
        format!("Replace with `{module}.lowlevel.checkpoint()`")
    }
}

/// ASYNC115
pub(crate) fn async_zero_sleep(checker: &Checker, call: &ExprCall) {
    if !(checker.semantic().seen_module(Modules::TRIO)
        || checker.semantic().seen_module(Modules::ANYIO))
    {
        return;
    }

    if call.arguments.len() != 1 {
        return;
    }

    let Some(qualified_name) = checker
        .semantic()
        .resolve_qualified_name(call.func.as_ref())
    else {
        return;
    };

    let Some(module) = AsyncModule::try_from(&qualified_name) else {
        return;
    };

    // Determine the correct argument name
    let arg_name = match module {
        AsyncModule::Trio => "seconds",
        AsyncModule::AnyIo => "delay",
        AsyncModule::AsyncIo => return,
    };

    let Some(arg) = call.arguments.find_argument_value(arg_name, 0) else {
        return;
    };

    match arg {
        Expr::NumberLiteral(ast::ExprNumberLiteral { value, .. }) => {
            if !matches!(value, Number::Int(Int::ZERO)) {
                return;
            }
        }
        _ => return,
    }

    let Some(qualified_name) = checker
        .semantic()
        .resolve_qualified_name(call.func.as_ref())
    else {
        return;
    };

    if let Some(module) = AsyncModule::try_from(&qualified_name) {
        let is_relevant_module = matches!(module, AsyncModule::Trio | AsyncModule::AnyIo);

        let is_sleep = is_relevant_module && matches!(qualified_name.segments(), [_, "sleep"]);

        if !is_sleep {
            return;
        }

        let mut diagnostic = checker.report_diagnostic(AsyncZeroSleep { module }, call.range());
        diagnostic.try_set_fix(|| {
            let (import_edit, binding) = checker.importer().get_or_import_symbol(
                &ImportRequest::import_from(&module.to_string(), "lowlevel"),
                call.func.start(),
                checker.semantic(),
            )?;
            let reference_edit =
                Edit::range_replacement(format!("{binding}.checkpoint"), call.func.range());
            let arg_edit = Edit::range_replacement("()".to_string(), call.arguments.range());
            Ok(Fix::applicable_edits(
                import_edit,
                [reference_edit, arg_edit],
                if checker.comment_ranges().intersects(call.range()) {
                    Applicability::Unsafe
                } else {
                    Applicability::Safe
                },
            ))
        });
    }
}
