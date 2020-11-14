class BasicConfig:
    pass


class DevelopmentConfig(BasicConfig):
    DEBUG = True


class ProductionConfig(BasicConfig):
    DEBUG = False


class TestingConfig(BasicConfig):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
