let 
    password = builtins.getEnv "MYSECRET";
in 
assert password != "";
{
  database = {
    host = builtins.getEnv "HOSTNAME";
    password = password;
    port = 5432;
    username = "admin";
  };
  features = {
    debug_mode = false;
    max_connections = 100;
  };
  logging = {
    level = "info";
    path = "/var/log/myapp";
  };
}
