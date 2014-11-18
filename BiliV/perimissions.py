from flask.ext.principal import RoleNeed, Permission

admin_permission = Permission(RoleNeed('admin'))
auth_permission = Permission(RoleNeed('authenticated'))
null_permission = Permission(RoleNeed('null'))