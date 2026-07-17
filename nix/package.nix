{
  pkgs,
  stdenvNoCC,
  makeWrapper,
  ...
}:
let
  python = (pkgs.python3.withPackages (
    python-pkgs: with python-pkgs; [
      bleak
      websockets
    ]
  ));
in
stdenvNoCC.mkDerivation {
  name = "pinetime-heartrate-server";
  version = "v1.0.0";

  src = ../src;

  nativeBuildInputs = [
    makeWrapper
  ];

  buildInputs = [ python ];

  postInstall = ''
    mkdir -pv $out/src
    cp -rv $src/* $out/src
    makeWrapper ${python}/bin/python3 $out/bin/pinetime-heartrate-server \
      --add-flags "$out/src/main.py"

    ls -lAh $out
  '';
}
