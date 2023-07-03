import stripe
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

class Trigram(models.Model):
    trigram_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a unique trigram"
        )
    chinese_character = models.CharField(
        max_length=2,
        db_comment="Original Chinese character representing the name of this trigram"
        )
    wade_giles_romanization = models.CharField(
        max_length=30,
        db_comment="Wade-Giles romanization of the name of this trigram"
        )
    pinyin_romanization = models.CharField(
        max_length=30,
        db_comment="Pinyin romanization of the name of this trigram"
        )
    english_translation = models.CharField(
        max_length=100,
        db_comment="English translation/interpretation of the name of this trigram"
        )
    trigram_symbol = models.CharField(
        max_length=1,
        db_comment="Unicode representation of the trigram"
        )
    description = models.TextField(
        db_comment="Verbose description of the trigram to provide context in readings"
        )
    family_relationship = models.CharField(
        max_length=30,
        db_comment="Designated family relationship for this trigram"
        )
    attribute = models.CharField(
        max_length=30,
        db_comment="Designated key attribute for this trigram"
        )
    symbolic_animal = models.CharField(
        max_length=30,
        db_comment="Designated symbolic animal for this trigram"
        )
    image_url = models.CharField(
        max_length=100,
        db_comment="URL path to the 'Dall-E 2'-generated image for this trigram"
        )
    primal_dir = models.CharField(
        max_length=2,
        db_comment="Cardinal direction representation of this trigram in the Primal Arrangement"
        )
    primal_season = models.CharField(
        max_length=30,
        db_comment="Seasonal representation of this trigram in the Primal Arrangement"
        )
    inner_world_dir = models.CharField(
        max_length=2,
        db_comment="Cardinal direction representation of this trigram in the Inner-World Arrangement"
        )
    inner_world_season = models.CharField(
        max_length=30,
        db_comment="Seasonal representation of this trigram in the Inner-World Arrangement"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "trigrams"
        db_table_comment = "A record for each unique trigram"
        ordering = ['trigram_id']

    def __str__(self):
        str_rep = f"Trigram {self.trigram_id} | {self.chinese_character} ('{self.pinyin_romanization}'): {self.english_translation}"
        return str_rep
    

class Hexagram(models.Model):
    hexagram_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a unique hexagram"
        )
    lower_trigram = models.ForeignKey(
        Trigram,
        on_delete=models.PROTECT,
        related_name='lower_trigram_ids',
        db_comment="Foreign key, references trigrams.trigram_id, represents the lower trigram of this hexagram"
        )
    upper_trigram = models.ForeignKey(
        Trigram,
        on_delete=models.PROTECT,
        related_name='upper_trigram_ids',
        db_comment="Foreign key, references trigrams.trigram_id, represents the upper trigram of this hexagram"
        )
    lower_nuclear_trigram = models.ForeignKey(
        Trigram,
        on_delete=models.PROTECT,
        related_name='lower_nuclear_trigram_ids',
        db_comment="Foreign key, references trigrams.trigram_id, represents the lower nuclear trigram of this hexagram"
        )
    upper_nuclear_trigram = models.ForeignKey(
        Trigram,
        on_delete=models.PROTECT,
        related_name='upper_nuclear_trigram_ids',
        db_comment="Foreign key, references trigrams.trigram_id, represents the upper nuclear trigram of this hexagram"
        )
    chinese_character = models.CharField(
        max_length=2,
        db_comment="Original Chinese character representing the name of this hexagram"
        )
    wade_giles_romanization = models.CharField(
        max_length=30,
        db_comment="Wade-Giles romanization of the name of this hexagram"
        )
    pinyin_romanization = models.CharField(
        max_length=30,
        db_comment="Pinyin romanization of the name of this hexagram"
        )
    english_translation = models.CharField(
        max_length=100,
        db_comment="English translation/interpretation of the name of this hexagram"
        )
    hexagram_symbol = models.CharField(
        max_length=1,
        db_comment="Unicode hexagram symbol representing this hexagram"
        )
    image_url = models.CharField(
        max_length=100,
        db_comment="URL path to the 'Dall-E 2'-generated image for this hexagram"
        )
    binary_value_string = models.CharField(
        max_length=6,
        default='000000',
        db_comment="The values of each line represented as a string, ordered bottom to top (eg. '011001')"
        )
    description = models.TextField(
        db_comment="Description of this hexagram"
        )
    judgment_text = models.TextField(
        db_comment="English translation of the written judgment for this hexagram"
        )
    judgment_interpretation = models.TextField(
        db_comment="Intepretation of this judgment offered by a commentator"
        )
    image_text = models.TextField(
        db_comment="English translation of the written image for this hexagram"
        )
    image_interpretation = models.TextField(
        db_comment="Intepretation of this image offered by a commentator"
        )
    full_change_text = models.TextField(
        blank=True,
        null=True,
        default=None,
        db_comment="Optional: special meaning of all the lines changing"
        )
    full_change_interpretation = models.TextField(
        blank=True,
        null=True,
        default=None,
        db_comment="Optional: interpretation of special meaning of all the lines changing"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "hexagrams"
        db_table_comment = "A record for each unique hexagram"
        ordering = ['hexagram_id']

    def __str__(self):
        str_rep = f"Hexagram {self.hexagram_id} | {self.chinese_character} ('{self.pinyin_romanization}'): {self.english_translation}"
        return str_rep
    

class HexagramLine(models.Model):
    hexagram_line_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a line within the context of a hexagram"
        )
    hexagram = models.ForeignKey(
        Hexagram,
        on_delete=models.PROTECT,
        related_name='hexagram_ids',
        db_comment="Foreign key, references hexagrams.hexagram_id, represents the hexagram this line belongs to"
        )
    position = models.SmallIntegerField(
        db_comment="Represents the position of this line in the hexagram, where 1 is the bottom and 6 is the top"
        )
    is_constituting_ruler = models.BooleanField(
        db_comment="TRUE if this line is the constituting ruler of its hexagram"
        )
    is_governing_ruler = models.BooleanField(
        db_comment="TRUE if this line is the governing ruler of its hexagram"
        )
    change_text = models.TextField(
        db_comment="English translation of the written interpretation of this line's change"
        )
    change_interpretation = models.TextField(
        db_comment="Intepretation of this judgment offered by a commentator"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )
    
    class Meta:
        db_table = "hexagram_lines"
        db_table_comment = "A record for each line within each hexagram"

    def __str__(self):
        str_rep = f"Hexagram Line {self.hexagram.hexagram_id}.{self.position} | {self.hexagram.english_translation}, line {self.position}"
        return str_rep
    ordering = ['hexagram_id', '-position']


class LineType(models.Model):
    line_type_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a type of line within the context of a changing hexagram"
        )
    name = models.CharField(
        max_length=10,
        db_comment="Name given to this line type (eg. 'Young Yin')"
        )
    image_url = models.CharField(
        max_length=100,
        db_comment="URL path to the line drawing of this line type"
        )
    description = models.TextField(
        db_comment="Description of this line type"
        )
    is_changing = models.BooleanField(
        db_comment="TRUE if this line type is changing, FALSE if this line is unchanging"
        )
    line_value = models.SmallIntegerField(
        db_comment="Represents the value that corresponds with this line type (6-9) as it relates to consulting the oracle with coins or yarrow stalks"
        )
    binary_value = models.SmallIntegerField(
        db_comment="Represents the binary value (0=yin, 1=yang) that corresponds with this line type as it relates to consulting the oracle with coins or yarrow stalks",
        default=0
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )
    
    class Meta:
        db_table = "line_types"
        db_table_comment = "A record for each type of line possible in an I Ching reading (ie. Old/Young Yin/Yang)"

    def __str__(self):
        str_rep = f"{self.name} ({self.line_value})"
        return str_rep


class Reading(models.Model):
    reading_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a unique I Ching reading from a given user"
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_comment="Foreign key, references Django's built-in users.id, represents the user that prepared this reading"
        )
    starting_hexagram = models.ForeignKey(
        Hexagram,
        on_delete=models.PROTECT,
        related_name='starting_hexagram_ids',
        db_comment="Foreign key, references hexgrams.hexagram_id, represents the starting hexagram of this reading"
        )
    resulting_hexagram = models.ForeignKey(
        Hexagram,
        blank=True,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        related_name='resulting_hexagram_ids',
        db_comment="Foreign key, references hexgrams.hexagram_id, represents the hexagram that results from the changes in this reading (if there are no changes, this value is null)"
        )
    value_string = models.CharField(
        max_length=6,
        default='888888',
        db_comment="The values of each line represented as a string, ordered bottom to top (eg. '677869')"
        )
    prompt = models.TextField(
        db_comment="User-entered prompt for this reading"
        )
    user_notes = models.TextField(
        blank=True,
        null=True,
        default=None,
        db_comment="Optional field that allows users to enter their own notes on this reading"
        )
    gpt_interpretation = models.TextField(
        blank=True,
        null=True,
        default=None,
        db_comment="Optional field resulting from the user generating an AI Interpretation for this reading"
        )
    is_public = models.BooleanField(
        default=False,
        db_comment="Readings are private by default, but can be made public so that others can access the reading via its unique URL."
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )
    
    class Meta:
        db_table = "readings"
        db_table_comment = "A record for each reading prepared by a user"
        ordering = ['-created_at']

    def __str__(self):
        if self.is_public:
            desc = f"public reading at {self.created_at}: {self.prompt}"
        else:
            desc = f"private reading at {self.created_at}"

        str_rep = f"{self.user.username} | {desc}"
        return str_rep
    

class UserDetail(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_comment="Foreign key, references Django's built-in users.id, represents the user that prepared this reading"
        )
    current_credits = models.IntegerField(
        default=0,
        db_comment="Represents this user's current number of credits available (1 credit can be exchanged for 1 AI-assisted interpretation on a reading)"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "user_details"
        db_table_comment = "A record for each user, with columns for different user-level details, always meant to represent the user's current state"
        ordering = ['user', '-updated_at']

    def __str__(self):
        str_rep = f"{self.user.username}'s Details ({self.current_credits} credits)"
        return str_rep


class UserPayment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_comment="Foreign key, references Django's built-in users.id, represents the user that is checking out"
        )
    is_success = models.BooleanField(
        default=False,
        db_comment="Boolean indicating whether or not the payment was successful."
        )
    stripe_checkout_id = models.CharField(
        max_length=500,
        db_comment="External identifier from Stripe representing the checkout."
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )
    
    class Meta:
        db_table = "user_payments"
        db_table_comment = "A historical record for each Stripe payment, including an initial record created at the time of user creation."
        ordering = ['user', '-created_at']
    
    def __str__(self):
        str_rep = f"{self.user.username}'s Payment at {self.created_at} ({self.stripe_checkout_id})"
        return str_rep


class CreditBundle(models.Model):
    num_credits = models.SmallIntegerField(
        db_comment = "Represents the number of AI Interpretation Credits included in this bundle."
        )
    price = models.SmallIntegerField(
        db_comment = "Represents the price in dollars of this bundle."
        )
    price_per_credit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_comment = "Represents the price in dollars of each credit in this bundle."
        )
    stripe_price_id = models.CharField(
        max_length=50,
        db_comment="External identifier from Stripe representing the unique Price object for this bundle."
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )
    
    class Meta:
        db_table = "credit_bundles"
        db_table_comment = "A record containing details for each credit bundle offered on visualiching.com."
    
    def __str__(self):
        str_rep = f"{self.num_credits} credit(s) for ${self.price} (${self.price_per_credit} per credit)"
        return str_rep


class UserCreditHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_comment="Foreign key, references Django's built-in users.id, represents the user that prepared this reading"
        )
    history_type = models.CharField(
        max_length=500,
        db_comment="String indicating the type of credit event this record represents (eg. 'Purchase', 'Redemption', etc.)"
        )
    credits_amount = models.IntegerField(
        db_comment="Integer representing the number of credits added to or deducted from the user's account"
        )
    user_payment = models.ForeignKey(
        UserPayment,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        db_comment="Only populated for 'Purchase' records, foreign key referencing user_payments.id record indicating the Stripe Checkout event related to this credit bundle purchase"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )
    
    class Meta:
        db_table = "user_credit_history"
        db_table_comment = "A historical record for each credit transaction, including credit purchases, credit grants from special offers, and credit redemptions from generating an AI-assisted interpretation for a reading"
        ordering = ['user', '-created_at']

    def __str__(self):
        str_rep = f"{self.user.username} | {self.history_type} at {self.created_at} ({self.credits_amount} credits)"
        return str_rep
    

@receiver(post_save, sender=User)
def create_user_detail(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)
    return