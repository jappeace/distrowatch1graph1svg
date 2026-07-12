# Decision: keep nixpkgs config in one file so shell.nix and nix/ci.nix import
# the exact same package set. Alternatives considered: inlining config at each
# import site (drifts out of sync). No unfree packages are needed here.
{
}
