import os
import django
import sys

# Setup Django environment
sys.path.append('e:/CODE/TEST/HNTH')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conference_manager.settings')
django.setup()

from schedule.models import Location, Conference, ConferenceLocation

def verify():
    print("Verifying Data...")
    
    # Check Location
    loc = Location.objects.filter(name="UBND Xã A").first()
    if loc:
        print(f"Location found: {loc.name}")
    else:
        print("Location 'UBND Xã A' NOT found.")
        # Create it for testing if missing
        loc = Location.objects.create(name="UBND Xã A", address="Address A")
        print("Created Location 'UBND Xã A'")

    # Check Conference
    conf = Conference.objects.first()
    if not conf:
        print("No conferences found. Creating one.")
        from django.utils import timezone
        conf = Conference.objects.create(title="Test Conf", start_time=timezone.now(), location="Main Hall")
    
    print(f"Using Conference: {conf.title}")

    # Check Link
    link = ConferenceLocation.objects.filter(conference=conf, location=loc).first()
    if link:
        print(f"Link found: {link.location.name} in {link.conference.title} with participants: {link.participants}")
    else:
        print("Link NOT found. Creating it.")
        link = ConferenceLocation.objects.create(conference=conf, location=loc, participants="Xã A, Xã B")
        print("Created Link.")

    # Verify Search Logic
    results = ConferenceLocation.objects.filter(participants__icontains="Xã B")
    print(f"Search for 'Xã B' returned {results.count()} results.")
    for res in results:
        print(f"- {res.conference.title}: {res.location.name} ({res.participants})")

if __name__ == "__main__":
    verify()
