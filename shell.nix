# Dev shell pinned through npins (same nixpkgs as nix/ci.nix). Enter with
# `nix-shell`; you get python3 with the app's runtime deps plus gnuclad and
# inkscape which __main__.py shells out to for the svg/png rendering.
{ pkgs ? import ./nix/pin.nix }:
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python: [
      python.requests
      python.beautifulsoup4
    ]))
    pkgs.gnuclad
    pkgs.inkscape
  ];
}
