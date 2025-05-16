use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use snix_eval::{Evaluation, Value as NixValue};
use std::env;

/// Internal helper: run Nix code `with builtins; toJSON (query)` with input bound.
fn run_nix_query(query: &str, input: NixValue) -> Result<String, String> {
    let evaluator = Evaluation::builder_impure()
        .add_builtins([("input", input)])
        .build();
    let cwd = env::current_dir().map_err(|e| format!("failed to get cwd: {}", e))?;
    let res = evaluator.evaluate(&query, Some(cwd));

    if !res.errors.is_empty() {
        let errs = res
            .errors
            .into_iter()
            .map(|e| e.to_string())
            .collect::<Vec<_>>()
            .join("\n");
        return Err(errs);
    }

    res.value
        .and_then(|v| match v {
            NixValue::String(nix_str) => Some(nix_str.to_string()),
            other => format!("{}", other).into(),
        })
        .ok_or_else(|| "evaluation did not return a JSON string".to_string())
}

/// Parse a Nix expression by converting it to JSON then delegating to Python's json.loads.
#[pyfunction]
fn loads(py: Python, expr: &str) -> PyResult<PyObject> {
    // Attempt to convert the Nix expression into a JSON string, map errors to Python ValueError
    let code = format!(r#"builtins.toJSON ({})"#, expr);
    let json_str = run_nix_query(&code, NixValue::Null)
        .map_err(|e| PyValueError::new_err(format!("nix parsing error: {}", e)))?;


    let json = py.import("json")?;
    let obj = json.call_method1("loads", (json_str,))?;
    let obj = json.call_method1("loads", (obj,))?;

    Ok(obj.into())
}

#[pyfunction]
fn dumps(py: Python, obj: PyObject) -> PyResult<String> {
    let json = py.import("json")?;
    let s: String = json.call_method1("dumps", (obj,))?.extract()?;
    let ns: NixValue = NixValue::from(s);
    let obj = run_nix_query("builtins.fromJSON builtins.input", ns)
        .map_err(|e| PyValueError::new_err(format!("dictionary parsing error: {}", e)))?;

    Ok(obj)
}

/// A Python module implemented in Rust.
#[pymodule]
fn nixeval(py: Python, m: Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(loads, py)?)?;
    m.add_function(wrap_pyfunction!(dumps, py)?)?;
    Ok(())
}
