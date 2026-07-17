{
  description = "PineTime HeartRate Server";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {nixpkgs, ...}:
  {
    devShells.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.mkShell {
      packages = with nixpkgs.legacyPackages.x86_64-linux; [
        (python3.withPackages (python-pkgs: with python-pkgs; [
          bleak
          websockets
        ]))
      ];
    };

    # TODO: all architectures
    packages.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.callPackage ./nix/package.nix {};
    nixosModules.default = import ./nix/module.nix;
  };
}
