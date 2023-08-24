from rest_framework import serializers


class PlantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    address = serializers.CharField(max_length=64)
    capacity = serializers.FloatField(required=False, allow_null=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def validate_latitude(self, latitude):
        if latitude < 32 or latitude > 39:
            raise serializers.ValidationError("위도의 범위가 잘못되었습니다.")
        return latitude

    def validate_longitude(self, longitude):
        if longitude < 124 or longitude > 131:
            raise serializers.ValidationError("경도의 범위가 잘못되었습니다.")
        return longitude

    def validate(self, data):
        return data


class InverterSerializer(serializers.Serializer):
    capacity = serializers.FloatField()
    tilt = serializers.FloatField()
    azimuth = serializers.FloatField()

    def validate(self, data):
        tilt = data.get("tilt")
        azimuth = data.get("azimuth")

        if tilt >= azimuth:
            raise serializers.ValidationError("경사각이 방위각보다 클 수 없습니다.")

        # 여기서 넘겨주는 값이 serializer.validated_data 이다.
        return data


class EssSerializer(serializers.Serializer):
    ess_cap = serializers.FloatField()
    ess_soc_l_lim = serializers.FloatField()
    ess_soc_h_lim = serializers.FloatField()
    pcs_cap = serializers.FloatField()
    pcs_h_lim = serializers.FloatField()
    ch_start = serializers.IntegerField()
    ch_end = serializers.IntegerField()
    dch_start = serializers.IntegerField()
    dch_end = serializers.IntegerField()

    ess_loss_eff = serializers.FloatField(required=False, allow_null=True)
    ess_reserve = serializers.FloatField(required=False, allow_null=True)
    ch_min_capacity = serializers.FloatField(required=False, allow_null=True)
    ch_max_capacity = serializers.FloatField(required=False, allow_null=True)
    dch_min_capacity = serializers.FloatField(required=False, allow_null=True)
    dch_max_capacity = serializers.FloatField(required=False, allow_null=True)
    ess_mfr = serializers.CharField(required=False, allow_null=True)
    pcs_mfr = serializers.CharField(required=False, allow_null=True)
    out_ctrl_feat = serializers.CharField(required=False, allow_null=True)

    def validate_ch_end(self, value):
        if value > 24:
            raise serializers.ValidationError("충전 종료시간은 24시를 넘을 수 없습니다.")
        return value

    def validate_dch_end(self, value):
        if value > 24:
            raise serializers.ValidationError("방전 종료시간은 24시를 넘을 수 없습니다.")
        return value

    def validate_ch_capacity(self, data):
        ch_min_capacity = data.get("ch_min_capacity")
        ch_max_capacity = data.get("ch_max_capacity")

        if (ch_min_capacity is None and ch_max_capacity is not None) or (
            ch_min_capacity is not None and ch_max_capacity is None
        ):
            raise serializers.ValidationError("충전 최소/최대 용량은 둘 다 값이 있거나 없어야 합니다.")
        elif ch_min_capacity and ch_max_capacity:
            if ch_min_capacity >= ch_max_capacity:
                raise serializers.ValidationError("충전 최소 용량은 최대용량보다 작아야 합니다.")

    def validate_dch_capacity(self, data):
        dch_min_capacity = data.get("dch_min_capacity")
        dch_max_capacity = data.get("dch_max_capacity")

        if (dch_min_capacity is None and dch_max_capacity is not None) or (
            dch_min_capacity is not None and dch_max_capacity is None
        ):
            raise serializers.ValidationError("방전 최소/최대 용량은 둘 다 값이 있거나 없어야 합니다.")
        elif dch_min_capacity and dch_max_capacity:
            if dch_min_capacity >= dch_max_capacity:
                raise serializers.ValidationError("방전 최소 용량은 최대용량보다 작아야 합니다.")

    def validate_soc_lim(self, data):
        ess_soc_l_lim = data.get("ess_soc_l_lim")
        ess_soc_h_lim = data.get("ess_soc_h_lim")

        if ess_soc_l_lim >= ess_soc_h_lim:
            raise serializers.ValidationError("soc 최소 용량은 최대 용량보다 작아야 합니다.")

    def validate(self, data):
        ch_start = data.get("ch_start")
        ch_end = data.get("ch_end")

        if ch_start >= ch_end:
            raise serializers.ValidationError("충전 시작 시간은 종료시간보다 작아야 합니다.")

        dch_start = data.get("dch_start")
        dch_end = data.get("dch_end")

        if dch_start >= dch_end:
            raise serializers.ValidationError("방전 시작 시간은 종료시간보다 작아야 합니다.")

        self.validate_ch_capacity(data)
        self.validate_dch_capacity(data)
        self.validate_soc_lim(data)

        return data
