# The real CI work lives here so it can be reproduced locally with a single
# `nix-build nix/ci.nix`. GitHub Actions only wraps this. It builds the exact
# python environment the app needs, byte-compiles every module to catch syntax
# errors, and runs the test suite as a sandboxed derivation.
{ pkgs ? import ./pin.nix }:
let
  # Runtime deps: fetchdists.py uses requests + beautifulsoup4, the rest of the
  # pipeline (graph/correct/svg) is stdlib only.
  pythonEnv = pkgs.python3.withPackages (packages: [
    packages.requests
    packages.beautifulsoup4
  ]);

  # Only the source tree, not the git metadata or a stray out/ cache dir.
  src = pkgs.lib.cleanSource ../.;

  checks = pkgs.runCommand "distrowatch1graph1svg-checks"
    { nativeBuildInputs = [ pythonEnv ]; }
    ''
      cp -r ${src}/. build
      chmod -R u+w build
      cd build

      echo "== byte-compiling every module =="
      python3 -m compileall -q *.py

      echo "== running test suite =="
      for test in test_*.py; do
        echo "--- $test ---"
        python3 "$test"
      done

      touch $out
    '';
in {
  # `nix-build nix/ci.nix -A checks` (or just the default below) runs everything.
  inherit checks pythonEnv;
}
