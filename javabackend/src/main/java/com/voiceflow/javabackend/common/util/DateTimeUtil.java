package com.voiceflow.javabackend.common.util;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;

public final class DateTimeUtil {

    private static final DateTimeFormatter ISO_FORMATTER = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    private DateTimeUtil() {
    }

    public static LocalDateTime nowUtc() {
        return LocalDateTime.now(ZoneOffset.UTC);
    }

    public static String formatIso(LocalDateTime dateTime) {
        return dateTime != null ? dateTime.format(ISO_FORMATTER) : null;
    }
}
