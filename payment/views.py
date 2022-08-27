from django.conf import settings
from django.shortcuts import redirect

from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_tracking.mixins import LoggingErrorsMixin

import payment.models
from .serializers import PaymentConfigSerializer

from zeep import Client

from account.permissions import ProfileComplete
from team.permissions import HasTeam

from .models import PaymentRequest, PaymentConfig


class PaymentRequestAPIView(LoggingErrorsMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, ProfileComplete, HasTeam)

    def post(self, request):
        client = Client(settings.ZARRIN_PAL_CLIENT)

        amount = PaymentConfig.objects.last().amount

        nahar = request.data.get('nahar', 0)

        if nahar == '1':
            amount += 160000

        payment_request = PaymentRequest.objects.create(
            user=request.user,
            amount=amount,
            team_name=request.user.team.name
        )

        result = client.service.PaymentRequest(
            settings.MERCHANT_ID,
            payment_request.amount,
            payment_request.description,
            payment_request.user.email,
            payment_request.user.profile.phone_number,
            payment_request.callback_url
        )

        if result.Status == 100:
            payment_request.authority = str(result.Authority)
            if len(payment_request.authority) != 36:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            payment_request.save()
            url = settings.ZARRIN_PAL_START_PAY + payment_request.authority

            return Response(data={'url': url}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyAPIView(LoggingErrorsMixin, GenericAPIView):

    def get(self, request):
        client = Client(settings.ZARRIN_PAL_CLIENT)

        if request.GET.get('Status') == 'OK':
            authority = request.GET['Authority']
            payment_request = get_object_or_404(PaymentRequest, authority=authority)
            result = client.service.PaymentVerification(
                settings.MERCHANT_ID,
                authority,
                payment_request.amount
            )
            if result.Status == 100:
                payment_request.ref_id = str(result.RefID)
                payment_request.user.profile.is_paid = True
                payment_request.user.profile.save()
                payment_request.save()

                return redirect(
                    f'https://aichallenge.ir/dashboard/payment'
                    f'?ref_id={payment_request.ref_id}'
                    f'&status=100&desc=با موفقیت پرداخت شد')
            if result.Status == 101:
                return redirect(
                    f'https://aichallenge.ir/dashboard/payment'
                    f'?status={str(result.Status)}&desc=تراکنش ثبت شد'
                )
            return redirect(
                f'https://aichallenge.ir/dashboard/payment'
                f'?status={str(result.Status)}&desc=تراکنش ناموفق'
            )

        return redirect(
            f'https://aichallenge.ir/dashboard/payment'
            f'?status=-1&desc=تراکنش ناموفق بود و یا توسط کاربر لغو شد'
        )


class PaymentConfigAPIView(LoggingErrorsMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentConfigSerializer

    def get(self, request):
        config = PaymentConfig.objects.all().last()

        nahar = request.GET.get('nahar', 0)

        amount = config.amount

        if nahar == '1':
            amount += 160000

        return Response(
            data={'config': {
                'amount': amount,
                'description': config.description,
            }},
            status=status.HTTP_200_OK
        )
