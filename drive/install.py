import frappe


def after_install():
    index_check = frappe.db.sql(
        """SHOW INDEX FROM `tabFile` WHERE Key_name = 'drive_file_name_fts_idx'"""
    )
    if not index_check:
        # sql_ddl, not sql: MariaDB commits implicitly on ALTER TABLE, and installing the app's
        # DocTypes has already written rows in this transaction, so frappe refuses plain DDL
        # here (ImplicitCommitError) and every fresh install-app failed (PR-Foundry/framework#317).
        frappe.db.sql_ddl(
            """ALTER TABLE `tabFile` ADD FULLTEXT INDEX drive_file_name_fts_idx (file_name)"""
        )
