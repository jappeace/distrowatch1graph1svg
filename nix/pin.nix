# Thin shim over npins so every consumer (shell.nix, nix/ci.nix) pulls the same
# pinned nixpkgs. Bump the pin with: npins update nixpkgs
import (import ../npins).nixpkgs { config = import ./config.nix; }
