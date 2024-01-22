from django.db import models, transaction
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from login.models import MyUser


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVER = 3
    TRANSFER_SEND = 4

    TRANSFER_TYPE_CHOICES = (
        (CHARGE, 'charge'),
        (PURCHASE, 'purchase'),
        (TRANSFER_RECEIVER, 'receiver'),
        (TRANSFER_SEND, 'transfer'),
    )

    positive_transaction = Sum(
        'transaction__amount',
        filter=Q(transaction__transaction_type__in=[1, 3])
    )
    negative_transaction = Sum(
        'transaction__amount',
        filter=Q(transaction__transaction_type__in=[2, 4])
    )

    user = models.ForeignKey(MyUser, related_name='transaction', on_delete=models.RESTRICT)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANSFER_TYPE_CHOICES, default=CHARGE)
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def sharj(cls, user, amount, transaction_type):
        return cls.objects.create(
            user=user,
            amount=amount,
            transaction_type=transaction_type
        )

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"

    @classmethod
    def get_report(cls):
        """show all users and their balance"""

        users = MyUser.objects.all().annotate(
            transaction_count=Count('transaction__id'),
            balance=Coalesce(cls.positive_transaction, 0) - Coalesce(cls.negative_transaction, 0)
        )

        return users

    @classmethod
    def get_report_by_user(cls, pk):
        """show one user and show balance"""
        user = MyUser.objects.filter(id=pk).aggregate(
            transaction_count=Count('transaction__id'),
            balance=Coalesce(cls.positive_transaction, 0) - Coalesce(cls.negative_transaction, 0)
        )
        return user

    @classmethod
    def get_list_transaction_by_user(cls, pk):
        """show one user and show balance"""
        list = Transaction.objects.filter(user_id=pk).all()
        return list

    @classmethod
    def user_balance(cls, user):
        positive_transaction = Sum(
            'amount',
            filter=Q(transaction_type__in=[1, 3])
        )
        negative_transaction = Sum(
            'amount',
            filter=Q(transaction_type__in=[2, 4])
        )

        user_balance = user.transaction.all().aggregate(
            balance=Coalesce(positive_transaction, 0) - Coalesce(negative_transaction, 0)
        )

        return user_balance.get('balance', 0)


class UserBalance(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.RESTRICT)
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = "Balances"

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.created_time}"

    @classmethod
    def record_user_by_id_balance(cls, pk):
        """show one user and show balance"""
        user = MyUser.objects.get(id=pk)
        exists = cls.objects.filter(user=user)

        if exists:
            old_user_balance = exists.first()
            new_balance = Transaction.user_balance(user)
            print(new_balance)
            old_user_balance.balance = new_balance
            old_user_balance.save()
            instance = cls.objects.get(user=user)

        else:
            instance = cls.objects.create(
                user=user,
                balance=Transaction.user_balance(user)
            )

        return instance

    @classmethod
    def record_user_balance(cls, user):
        """show one user and show balance"""
        user_balance = user.transaction.all().aggregate(
            balance=Coalesce(cls.positive_transaction, 0) - Coalesce(cls.negative_transaction, 0)
        )
        instance = cls.objects.create(
            user=user,
            balance=user_balance['balance']
        )
        return instance

    @classmethod
    def record_all_user_balance(cls):
        users = MyUser.objects.all()
        for user in users:
            cls.record_user_balance(user)


class TransferTransaction(models.Model):
    sender_transaction = models.ForeignKey(
        Transaction, related_name='sender_transaction', on_delete=models.RESTRICT)
    received_transaction = models.ForeignKey(
        Transaction, related_name='received_transaction', on_delete=models.RESTRICT)
    amount = models.BigIntegerField()
    sender_name = models.CharField(max_length=48)
    received_name = models.CharField(max_length=48)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_transaction} - {self.amount} - {self.received_transaction}"

    @classmethod
    def get_list_transfer_transaction_by_user(cls, pk):
        """show one user and show balance"""
        user = MyUser.objects.filter(pk=pk).first()
        mobile = str(user.mobile)

        list = TransferTransaction.objects.filter(sender_name=mobile).select_related('sender_transaction').all()
        return list

    @classmethod
    def get_received_list_transfer_transaction_by_user(cls, pk):
        """show one user and show balance"""
        user = MyUser.objects.filter(pk=pk).first()
        mobile = str(user.mobile)
        list = TransferTransaction.objects.filter(received_name=mobile).select_related('received_transaction').all()
        return list

    @classmethod
    def transfer(cls, sender_pk, mobile_receiver, amount):
        sender = MyUser.objects.filter(id=sender_pk).first()
        receiver = MyUser.objects.filter(mobile=mobile_receiver).first()
        sender_name = sender.mobile
        received_name = receiver.mobile
        amount = int(amount)

        if Transaction.user_balance(sender) < amount:
            return "transaction not Allowed, insufficient balance"

        with transaction.atomic():
            # 1) yek trakonesh baraye kasi ke ersal mablagh dashte
            send_transaction = Transaction.objects.create(
                user=sender, transaction_type=Transaction.TRANSFER_SEND, amount=amount
            )
            # 2) yek trakonesh baraye kasi ke daryaftkonande mablagh bode
            received_transaction = Transaction.objects.create(
                user=receiver, transaction_type=Transaction.TRANSFER_RECEIVER, amount=amount
            )
            # 3) in 2 mored yani ersal konande va daryaft konande ba ham link mishan
            instance = cls.objects.create(
                sender_transaction=send_transaction, sender_name=sender_name,
                received_transaction=received_transaction, received_name=received_name,
                amount=amount
            )
            # 4) balance sender ro update mikonim
            UserBalance.record_user_by_id_balance(sender.pk)

            # 5) balance reciver ro update mikonim
            UserBalance.record_user_by_id_balance(receiver.pk)
        return instance


class UserScore(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.user} - {self.score}"

    @classmethod
    def change_score(cls, user, score):
        instance = cls.objects.select_for_update().filter(user=user)
        with transaction.atomic():
            if not instance.exists():
                instance = cls.objects.create(user=user, score=0)
            else:
                instance = instance.first()

            instance.score += score
            instance.save()

        return instance

    @classmethod
    def user_score(cls, pk, score):
        user = MyUser.objects.get(pk=pk)
        instance = cls.change_score(user, score)
        return instance


