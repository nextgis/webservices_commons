
class NextGisIdScopes:

    # NGID
    USER_INFO_READ = 'user_info.read'
    USER_INFO_WRITE = 'user_info.write'

    # QMS
    QMS_PUBLIC_WRITE = 'qms.public.write'
    QMS_PRIVATE_READ = 'qms.private.read'
    QMS_PRIVATE_WRITE = 'qms.private.write'

    @staticmethod
    def default_scope(cls):
        return cls.USER_INFO_READ

    @staticmethod
    def as_dict(cls):
        return {
            cls.USER_INFO_READ: 'Read user info',
            cls.USER_INFO_WRITE: 'Write user info',
            cls.QMS_PUBLIC_WRITE: 'Write public resources to QMS',
            cls.QMS_PRIVATE_READ: 'Read private resources to QMS',
            cls.QMS_PRIVATE_WRITE: 'Write private resources to QMS',
        }