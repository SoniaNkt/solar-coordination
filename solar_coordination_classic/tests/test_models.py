from django.test import TestCase, Client
from solar_coordination_classic.models import Condition, SolarGenerationProfile, SolarGeneration, StudyRun, User, StudyRunAllocation, Booking, ComfortProfile, ComfortCostSlot, Participant
import datetime

class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.condition = Condition.objects.create(
            ui_type = "Chatbot First",
            group_size = 9,
            active = False,
        )

        cls.solar_generation_profile = SolarGenerationProfile.objects.create(
            name = "Overcast Autumn Day",
        ) 

        cls.solar_generation = SolarGeneration.objects.create(
            hour = "10",
            amount = 290,
            solar_generation_profile = cls.solar_generation_profile
        )    

        cls.study_run = StudyRun.objects.create(
            completed =True,
            condition = cls.condition,
            solar_generation_profile = cls.solar_generation_profile
        )     

        cls.user = User.objects.create(
            username ="Test Username",
            password = "T3stPassW0rd!",
        ) 

        cls.study_run_allocation = StudyRunAllocation.objects.create(
            study_run = cls.study_run,
            user = cls.user
        )     

        cls.booking = Booking.objects.create(
            name= "Test activity",
            hour = 12,
            amount = 230,
            created_at = datetime.datetime.now(),
            modified_at = datetime.datetime.now(),
            user = cls.user
        )  

        cls.comfort_profile = ComfortProfile.objects.create(
            name = "8am to 4pm",
        )  

        cls.comfort_cost_slot = ComfortCostSlot.objects.create(
            hour = 10,
            cost = 0.50,
            comfort_profile = cls.comfort_profile
        ) 

        cls.participant = Participant.objects.create(
            user = cls.user,
            comfort_profile = cls.comfort_profile,
            condition = cls.condition
        ) 

    # Condition

    def test_condition_field_nomenclature(self):
        condition = Condition.objects.get(id=self.condition.id)
        field_ui_type = condition._meta.get_field('ui_type').verbose_name
        field_group_size = condition._meta.get_field('group_size').verbose_name
        field_active = condition._meta.get_field('active').verbose_name

        self.assertEqual(field_ui_type, 'ui type')
        self.assertEqual(field_group_size, 'group size')
        self.assertEqual(field_active, 'active')

    def test_condition_duplicate(self):
        condition = Condition.objects.get(id=self.condition.id)
        duplicate_condition = Condition(
            ui_type="Chatbot First",
            group_size=9,
        )

        with self.assertRaises(Exception):
            duplicate_condition.save()

    # Solar Generation Profile

    def test_solar_generation_profile_field_nomenclature(self):
        solar_generation_profile = SolarGenerationProfile.objects.get(id=self.solar_generation_profile.id)
        field_name = solar_generation_profile._meta.get_field('name').verbose_name

        self.assertEqual(field_name, 'name')

    # Solar Generation

    def test_solar_generation_field_nomenclature(self):
        solar_generation = SolarGeneration.objects.get(id=self.solar_generation.id)
        field_hour = solar_generation._meta.get_field('hour').verbose_name
        field_amount = solar_generation._meta.get_field('amount').verbose_name

        self.assertEqual(field_hour, 'hour')
        self.assertEqual(field_amount, 'amount')

    def test_solar_generation_relationship(self):
        solar_generation = SolarGeneration.objects.get(id=self.solar_generation.id)
        self.assertEqual(solar_generation.solar_generation_profile, self.solar_generation_profile)

    # Study Run

    def test_study_run_field_nomenclature_and_relationships(self):
        study_run = StudyRun.objects.get(id=self.study_run.id)
        field_completed = study_run._meta.get_field('completed').verbose_name

        self.assertEqual(field_completed, 'completed')

    def test_study_run_relationships(self):
        study_run = StudyRun.objects.get(id=self.study_run.id)
        self.assertEqual(study_run.condition, self.condition)
        self.assertEqual(study_run.solar_generation_profile, self.solar_generation_profile)
        
    # User

    def test_user_field_nomenclature(self):
        user = User.objects.get(id=self.user.id)
        field_username = user._meta.get_field('username').verbose_name
        field_password = user._meta.get_field('password').verbose_name

        self.assertEqual(field_username, 'username')
        self.assertEqual(field_password, 'password')

    # Study Run Allocation

    def test_study_run_allocation_relationships(self):
        study_run_allocation = StudyRunAllocation.objects.get(id=self.study_run_allocation.id)
        self.assertEqual(study_run_allocation.user, self.user)

    # Booking

    def test_booking_field_nomenclature(self):
        booking = Booking.objects.get(id=self.booking.id)
        field_name = booking._meta.get_field('name').verbose_name
        field_hour = booking._meta.get_field('hour').verbose_name
        field_amount = booking._meta.get_field('amount').verbose_name
        field_created_at = booking._meta.get_field('created_at').verbose_name
        field_modified_at = booking._meta.get_field('modified_at').verbose_name


        self.assertEqual(field_name, 'name')
        self.assertEqual(field_hour, 'hour')
        self.assertEqual(field_amount, 'amount')
        self.assertEqual(field_created_at, 'created at')
        self.assertEqual(field_modified_at, 'modified at')
        
    def test_booking_relationship(self):
        booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(booking.user, self.user)

    # Comfort Profile

    def test_comfort_profile_field_nomenclature(self):
        comfort_profile = ComfortProfile.objects.get(id=self.comfort_profile.id)
        field_name = comfort_profile._meta.get_field('name').verbose_name

        self.assertEqual(field_name, 'name')

    # Comfort Cost Slot

    def test_comfort_cost_slot_field_nomenclature(self):
        comfort_cost_slot = ComfortCostSlot.objects.get(id=self.comfort_cost_slot.id)
        field_hour = comfort_cost_slot._meta.get_field('hour').verbose_name
        field_cost = comfort_cost_slot._meta.get_field('cost').verbose_name

        self.assertEqual(field_hour, 'hour')
        self.assertEqual(field_cost, 'cost')
        
    def test_comfort_cost_slot_relationship(self):
        comfort_cost_slot = ComfortCostSlot.objects.get(id=self.comfort_cost_slot.id)
        self.assertEqual(comfort_cost_slot.comfort_profile, self.comfort_profile)

    # Participant

    def test_participant_relationship(self):
        participant = Participant.objects.get(id=self.participant.id)
        self.assertEqual(participant.user, self.user)
        self.assertEqual(participant.condition, self.condition)
        self.assertEqual(participant.comfort_profile, self.comfort_profile)


