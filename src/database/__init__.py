"""Database initialization and utilities."""

import os
from src.database.models import db, User, KBArticle, Setting


def init_db(app):
    """Initialize database."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        # Create default data
        seed_database()


def seed_database():
    """Seed database with initial data."""
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@pkpro.local',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')  # Default password - CHANGE THIS!
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created (username: admin, password: admin123)")
    
    # Create default KB articles
    kb_count = KBArticle.query.count()
    if kb_count == 0:
        default_articles = [
            KBArticle(
                category='windows_server',
                title='วิธีเพิ่ม User ใน Active Directory',
                content=''''\n1. เปิด Active Directory Users and Computers\n2. Navigate to Organizational Unit\n3. Right-click → New → User\n4. Fill in user information\n5. Set password\n6. Finish\n\nหรือใช้ PowerShell:\nNew-ADUser -Name "John Doe" -SamAccountName "jdoe" -GivenName "John" -Surname "Doe" -AccountPassword (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force) -Enabled $true\n''',
                tags='Active Directory, User Management, Windows Server',
                language='th',
                is_featured=True
            ),
            KBArticle(
                category='troubleshooting',
                title='การแก้ไข Connection Timeout',
                content=''''\n### สาเหตุ:\n- Network issue\n- Firewall blocking\n- Service down\n- Configuration error\n\n### การแก้ไข:\n1. Check network connectivity\n2. Verify firewall rules\n3. Check service status\n4. Review configuration\n5. Restart service if needed\n''',
                tags='Troubleshooting, Network, Connection',
                language='th',
                is_featured=True
            ),
            KBArticle(
                category='networking',
                title='DNS Configuration Best Practices',
                content=''''\n### DNS Servers:\n- Primary: 8.8.8.8\n- Secondary: 8.8.4.4\n\n### Setting DNS via PowerShell:\nSet-DnsClientServerAddress -InterfaceIndex 12 -ServerAddresses "8.8.8.8", "8.8.4.4"\n\n### Verification:\nResolve-DnsName google.com\n''',
                tags='DNS, Networking, Configuration',
                language='th',
                is_featured=False
            )
        ]
        
        for article in default_articles:
            db.session.add(article)
        
        db.session.commit()
        print(f"✅ Created {len(default_articles)} default KB articles")
    
    # Create default settings
    setting_count = Setting.query.count()
    if setting_count == 0:
        default_settings = [
            Setting(
                key='app_name',
                value='AI IT Technician Assistant',
                description='Application name'
            ),
            Setting(
                key='app_version',
                value='1.0.0',
                description='Application version'
            ),
            Setting(
                key='default_language',
                value='th',
                description='Default language (th/en)'
            ),
            Setting(
                key='max_upload_size',
                value='10485760',  # 10MB
                description='Max upload file size in bytes'
            )
        ]
        
        for setting in default_settings:
            db.session.add(setting)
        
        db.session.commit()
        print(f"✅ Created {len(default_settings)} default settings")


def reset_database(app):
    """Reset database - WARNING: Deletes all data!"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()
        print("✅ Database reset complete")
