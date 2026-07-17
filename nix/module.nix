{ config, lib, pkgs, ... }:
let
  dataDir = "/var/lib/pinetime-heartrate";
  cfg = config.services.pinetimeHeartrate;
in
{
  options.services.pinetimeHeartrate = {
    enable = lib.mkEnableOption "Enable the PineTime Heartrate server.";
    package = lib.mkOption {
      type = lib.types.package;
      default = pkgs.callPackage ./package.nix {};
    };

    host = lib.mkOption {
      type = lib.types.str;
      default = "localhost";
      description = "The address to host the WebSocket server on.";
    };
    port = lib.mkOption {
      type = lib.types.int;
      default = 8765;
      description = "The port to host the WebSocket server on.";
    };
    openFirewall = lib.mkOption {
      type = lib.types.bool;
      default = false;
      description = "Whether to open the required firewall ports in the firewall.";
    };
    deviceName = lib.mkOption {
      type = lib.types.str;
      default = "InfiniTime";
      description = "The name of the Bluetooth device to scan for.";
    };
  };

  config = lib.mkIf cfg.enable {
    systemd.services.pinetimeHeartrate = {
      enable = true;
      description = "PineTime Heartrate Server";

      wants = [ "bluetooth.target" ];
      after = [ "bluetooth.target" ];
      wantedBy = [ "multi-user.target" ];

      environment = {
        HOST = cfg.host;
        PORT = toString cfg.port;
        DEVICE_NAME = cfg.deviceName;
      };

      unitConfig = {};
      serviceConfig = {
        Type = "simple";
        ExecStart = "${cfg.package}/bin/pinetime-heartrate-server";
        Restart = "always";
        RestartSec = 5;

        User = baseNameOf dataDir;
        Group = baseNameOf dataDir;

        WorkingDirectory = dataDir;
        StateDirectory = baseNameOf dataDir;
        StateDirectoryMode = "0700";

        # hardening
        ProtectSystem = "strict";
        PrivateTmp = true;
        PrivateDevices = true;
        ProtectKernelTunables = true;
        ProtectControlGroups = true;
        RestrictSUIDSGID = true;
        PrivateMounts = true;
        ProtectKernelModules = true;
        ProtectKernelLogs = true;
        ProtectHostname = true;
        ProtectClock = true;
        ProtectProc = "invisible";
        ProcSubset = "pid";
        RestrictNamespaces = true;
        RemoveIPC = true;
        UMask = "0077";
        NoNewPrivileges = true;
        LockPersonality = true;
        RestrictRealtime = true;
      };
    };

    users.groups.${baseNameOf dataDir} = {};
    users.users.${baseNameOf dataDir} = {
      description = "Service user for PineTime Heartrate Server";
      group = baseNameOf dataDir;
      home = dataDir;
      isSystemUser = true;
    };

    networking.firewall = lib.mkIf cfg.openFirewall {
      allowedTCPPorts = [ cfg.port ];
    };
  };
}
