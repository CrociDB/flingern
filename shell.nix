{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.python3
    pkgs.uv
    
    pkgs.libjpeg
    pkgs.zlib
  ];

  shellHook = ''
    echo "flingern development shell"
    
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
      pkgs.libjpeg
      pkgs.zlib
    ]}:$LD_LIBRARY_PATH
  '';
}
