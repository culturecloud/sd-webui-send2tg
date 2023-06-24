import launch

if not launch.is_installed("requests"):
    launch.run_pip("install --upgrade requests", "requirements for Send2TG")
