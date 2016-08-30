{ pkgs ? import <nixpkgs> {}
}:

with pkgs;

let
  pyEnv = [ python27Full ]
          ++ (with python27Packages;
             [ pip virtualenv
               pillow
             ]
          );


  systemDeps = [
    cacert
    libffi
    openssl
    pkgconfig
    sqlite
    zlib
  ];

  devDeps = [ file which ];

  allDeps = pyEnv ++ systemDeps ++ devDeps;

in

stdenv.mkDerivation {
  name = "cloudmesh_client_env";
  buildInputs = allDeps;
  shellHook = ''
    export SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt
    test -d venv || virtualenv venv
    source venv/bin/activate
  '';
}
