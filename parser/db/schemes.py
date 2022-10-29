from sqlalchemy import create_engine, Column, String, Integer, Text, JSON
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine("mysql://admin:admin@localhost:3306/test")


class User(Base):
    __tablename__ = 'parsed_pets'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=True)
    animal = Column(Integer, nullable=True)
    type = Column(Integer, nullable=True)
    sex = Column(Integer, nullable=True)
    created_at = Column(Integer, nullable=True)
    updated_at = Column(Integer, nullable=True)
    happened_at = Column(Integer, nullable=True)
    website = Column(Integer, nullable=True)
    ws_id = Column(String(length=100), nullable=True)
    phone = Column(String(length=50), nullable=True)
    email = Column(String(length=250), nullable=True)
    author = Column(String(length=250), nullable=True)
    address = Column(String(length=250), nullable=True)
    descr = Column(Text, nullable=True)
    pics = Column(JSON, nullable=True)


sql_expression = '''
CREATE TABLE `parsed_pets` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `status` INT(1) NULL DEFAULT NULL COMMENT '-1 - плохое, 0 - новый, 1 - обработано',
  `animal` INT(1) NULL DEFAULT NULL COMMENT '1 - dog, 2 - cat',
  `type` INT(1) NULL DEFAULT NULL COMMENT '1 - propal, 2 - nashel',
  `sex` INT(1) NULL DEFAULT NULL COMMENT '1 - unknown, 2 - male, 3 - female',
  `created_at` INT(11) NULL DEFAULT NULL,
  `updated_at` INT(11) NULL DEFAULT NULL,
  `happened_at` INT(11) NULL DEFAULT NULL,
  `website` INT(2) NULL DEFAULT NULL COMMENT 'ид вебсайта откуда парсим',
  `ws_id` VARCHAR(100) NULL DEFAULT NULL COMMENT 'website pet id' COLLATE 'utf8mb4_unicode_ci',
  `phone` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
  `email` VARCHAR(250) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
  `author` VARCHAR(250) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
  `address` VARCHAR(250) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
  `descr` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
  `pics` JSON DEFAULT NULL',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `website_ws_id` (`website`, `ws_id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;
'''

# try:
#     result = engine.execute(sql_expression)
# except OperationalError:
#     pass

