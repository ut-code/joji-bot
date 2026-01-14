{ pkgs }:
pkgs.mkShell {
  # Add build dependencies
  packages = with pkgs; [
    uv
  ];

  # Add environment variables
  env = { };

  # Load custom bash code
  shellHook = ''

  '';
}
