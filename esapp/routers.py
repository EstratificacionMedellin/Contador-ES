class SegundaDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.db_table == 'zcatt_sgto_trmte':
            return 'secundaria'
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'secundaria':
            return False
        return None
