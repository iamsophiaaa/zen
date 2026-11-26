from django.core.management.base import BaseCommand
from core.models import Table  # Replace 'your_app' with your actual app name


class Command(BaseCommand):
    help = "Creates a specified number of Table objects in the database"

    def add_arguments(self, parser):
        # Named argument with a default fallback of 1
        parser.add_argument(
            "-n",'--num',
            type=int,
            default=10,
            help="The number of tables to create",
        )

    def handle(self, *args, **options):
        count = options["num"]
       
        # Bulk create for efficiency
        for i in range(1, count + 1):
            table, created = Table.objects.get_or_create(
                name=f'Table {i}'
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created {table}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'{table} already exists'))
        
            self.stdout.write(
                self.style.SUCCESS(f'Created {table}')
            )
            
        self.stdout.write(self.style.SUCCESS(f'Done. {count} tables created.')
        )
