{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    rustc
    cargo
    maturin
    python312
    python312Packages.pip
    python312Packages.virtualenv
  ];

  # Automatically create and activate a virtualenv
  shellHook = ''
    if [ ! -d .venv ]; then
      python -m virtualenv .venv
    fi
    source .venv/bin/activate
  '';
}