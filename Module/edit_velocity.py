import yaml

def update_velocity_settings(secret):
    with open("paper.global.yml", 'r') as file:
        config = yaml.safe_load(file)

    config['proxies']['velocity']['enabled'] = True
    config['proxies']['velocity']['online-mode'] = True
    config['proxies']['velocity']['secret'] = secret

    with open("paper.global.yml", 'w') as file:
        yaml.safe_dump(config, file)
