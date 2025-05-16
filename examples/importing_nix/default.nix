let 
  hello = "Hello";
  world = [ "w" "o" "r" "l" "d"];
in 
"${hello} ${builtins.foldl' (x: y: x + y) "" world}"