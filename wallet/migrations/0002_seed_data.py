from django.db import migrations

def seed_emotion(apps, schema_editor):
    WalletEmotion = apps.get_model("wallet", "WalletEmotion")
    WalletEmotion.objects.bulk_create([
        WalletEmotion(wallet_emotion_type='happy', wallet_emotion_id=1),
        WalletEmotion(wallet_emotion_type='sad', wallet_emotion_id=2),
        WalletEmotion(wallet_emotion_type='angry', wallet_emotion_id=3),
        WalletEmotion(wallet_emotion_type='anxious', wallet_emotion_id=4),
        WalletEmotion(wallet_emotion_type='comfort', wallet_emotion_id=5),
        WalletEmotion(wallet_emotion_type='satisfied', wallet_emotion_id=6),
        WalletEmotion(wallet_emotion_type='tired', wallet_emotion_id=7),
        WalletEmotion(wallet_emotion_type='expected', wallet_emotion_id=8),
    ])

def seed_category(apps, schema_editor):
    WalletCategory = apps.get_model("wallet", "WalletCategory")
    WalletCategory.objects.bulk_create([
        WalletCategory(wallet_category_type='food', wallet_category_id=1),
        WalletCategory(wallet_category_type='living', wallet_category_id=2),
        WalletCategory(wallet_category_type='transport', wallet_category_id=3),
        WalletCategory(wallet_category_type='health', wallet_category_id=4),
        WalletCategory(wallet_category_type='education', wallet_category_id=5),
        WalletCategory(wallet_category_type='shopping', wallet_category_id=6),
        WalletCategory(wallet_category_type='culture', wallet_category_id=7),
        WalletCategory(wallet_category_type='finance', wallet_category_id=8),
        WalletCategory(wallet_category_type='salary', wallet_category_id=9),
        WalletCategory(wallet_category_type='bonus', wallet_category_id=10),
        WalletCategory(wallet_category_type='pocket_money', wallet_category_id=11),
        WalletCategory(wallet_category_type='side_job', wallet_category_id=12),
        WalletCategory(wallet_category_type='investment', wallet_category_id=13),
        WalletCategory(wallet_category_type='refund', wallet_category_id=14),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_emotion),
        migrations.RunPython(seed_category),
    ]
