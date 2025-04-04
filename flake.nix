{
  description = "Flake for pygame development";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };
  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python3
          (python3.withPackages (ps: with ps; [ pygame ]))
          # Maybe switch to community edition?
          black

          #SDL2
          #SDL2_image
          #SDL2_ttf
        ];
      };
    };
}
