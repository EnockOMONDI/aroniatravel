from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connection
import sys


class Command(BaseCommand):
    help = 'Safely run migrations with production database confirmation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Specific app to migrate',
        )
        parser.add_argument(
            '--fake',
            action='store_true',
            help='Mark migrations as run without actually running them',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what migrations would be applied without running them',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompts (use with extreme caution)',
        )

    def handle(self, *args, **options):
        # Check if we're using production database
        production_db = getattr(settings, 'PRODUCTION_DB', False)
        
        if production_db:
            self.stdout.write(
                self.style.WARNING('⚠️  WARNING: You are about to run migrations on the PRODUCTION database!')
            )
            self.stdout.write(
                self.style.WARNING('⚠️  Database: NeonDB PostgreSQL')
            )
            
            # Show current database info
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database(), current_user;")
                db_info = cursor.fetchone()
                self.stdout.write(f"Database: {db_info[0]}, User: {db_info[1]}")
            
            if not options['force']:
                # Show what migrations would be applied
                self.stdout.write(self.style.HTTP_INFO('\n📋 Checking migration status...'))
                call_command('showmigrations', verbosity=1)
                
                # Confirmation prompt
                self.stdout.write(self.style.WARNING('\n⚠️  Are you sure you want to proceed?'))
                self.stdout.write('Type "yes" to continue, or anything else to cancel:')
                
                confirmation = input().strip().lower()
                if confirmation != 'yes':
                    self.stdout.write(self.style.ERROR('❌ Migration cancelled.'))
                    return
        
        # Run the migration
        try:
            if options['dry_run']:
                self.stdout.write(self.style.HTTP_INFO('🔍 DRY RUN - No actual migrations will be applied'))
                call_command('showmigrations', verbosity=2)
            else:
                migrate_args = []
                if options['app']:
                    migrate_args.append(options['app'])
                if options['fake']:
                    migrate_args.append('--fake')
                
                self.stdout.write(self.style.SUCCESS('🚀 Running migrations...'))
                call_command('migrate', *migrate_args, verbosity=2)
                self.stdout.write(self.style.SUCCESS('✅ Migrations completed successfully!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Migration failed: {e}'))
            sys.exit(1)
