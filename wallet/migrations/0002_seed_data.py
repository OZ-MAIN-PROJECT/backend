from django.db import migrations

def seed_emotion(apps, schema_editor):
    WalletEmotion = apps.get_model("wallet", "WalletEmotion")
    WalletEmotion.objects.bulk_create([
        WalletEmotion(wallet_emotion_type='행복', wallet_emotion_id=1),
        WalletEmotion(wallet_emotion_type='슬픔', wallet_emotion_id=2),
        WalletEmotion(wallet_emotion_type='분노', wallet_emotion_id=3),
        WalletEmotion(wallet_emotion_type='불안', wallet_emotion_id=4),
        WalletEmotion(wallet_emotion_type='위로', wallet_emotion_id=5),
        WalletEmotion(wallet_emotion_type='만족', wallet_emotion_id=6),
        WalletEmotion(wallet_emotion_type='지침', wallet_emotion_id=7),
        WalletEmotion(wallet_emotion_type='기대', wallet_emotion_id=8),
    ])

def seed_category(apps, schema_editor):
    WalletCategory = apps.get_model("wallet", "WalletCategory")
    WalletCategory.objects.bulk_create([
        WalletCategory(wallet_category_type='식비', wallet_category_id=1),
        WalletCategory(wallet_category_type='생활', wallet_category_id=2),
        WalletCategory(wallet_category_type='교통/차량', wallet_category_id=3),
        WalletCategory(wallet_category_type='건강', wallet_category_id=4),
        WalletCategory(wallet_category_type='교육', wallet_category_id=5),
        WalletCategory(wallet_category_type='쇼핑', wallet_category_id=6),
        WalletCategory(wallet_category_type='여가/문화', wallet_category_id=7),
        WalletCategory(wallet_category_type='금융', wallet_category_id=8),
        WalletCategory(wallet_category_type='급여', wallet_category_id=9),
        WalletCategory(wallet_category_type='상여/보너스', wallet_category_id=10),
        WalletCategory(wallet_category_type='용돈', wallet_category_id=11),
        WalletCategory(wallet_category_type='부수입', wallet_category_id=12),
        WalletCategory(wallet_category_type='투자수익', wallet_category_id=13),
        WalletCategory(wallet_category_type='환급', wallet_category_id=14),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_emotion),
        migrations.RunPython(seed_category),
    ]

