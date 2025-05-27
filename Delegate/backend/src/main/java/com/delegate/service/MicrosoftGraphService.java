package com.delegate.service;

import com.microsoft.graph.models.AutomaticRepliesMailTips;
import com.microsoft.graph.models.AutomaticRepliesSetting;
import com.microsoft.graph.models.DateTimeTimeZone;
import com.microsoft.graph.models.MailboxSettings;
import com.microsoft.graph.requests.GraphServiceClient;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

@Service
@RequiredArgsConstructor
public class MicrosoftGraphService {
    private final GraphServiceClient graphClient;

    @Value("${microsoft.graph.timezone}")
    private String timezone;

    public void setAutomaticReplies(String userId, String message, LocalDateTime startTime, LocalDateTime endTime) {
        MailboxSettings mailboxSettings = new MailboxSettings();
        AutomaticRepliesSetting automaticRepliesSetting = new AutomaticRepliesSetting();
        
        automaticRepliesSetting.setStatus(AutomaticRepliesMailTips.AUTOMATIC_REPLIES);
        automaticRepliesSetting.setInternalReplyMessage(message);
        automaticRepliesSetting.setExternalReplyMessage(message);
        
        DateTimeTimeZone startDateTime = new DateTimeTimeZone();
        startDateTime.setDateTime(startTime.format(DateTimeFormatter.ISO_DATE_TIME));
        startDateTime.setTimeZone(timezone);
        
        DateTimeTimeZone endDateTime = new DateTimeTimeZone();
        endDateTime.setDateTime(endTime.format(DateTimeFormatter.ISO_DATE_TIME));
        endDateTime.setTimeZone(timezone);
        
        automaticRepliesSetting.setScheduledStartDateTime(startDateTime);
        automaticRepliesSetting.setScheduledEndDateTime(endDateTime);
        
        mailboxSettings.setAutomaticRepliesSetting(automaticRepliesSetting);
        
        graphClient.users(userId)
            .mailboxSettings()
            .buildRequest()
            .patch(mailboxSettings);
    }

    public void clearAutomaticReplies(String userId) {
        MailboxSettings mailboxSettings = new MailboxSettings();
        AutomaticRepliesSetting automaticRepliesSetting = new AutomaticRepliesSetting();
        automaticRepliesSetting.setStatus(AutomaticRepliesMailTips.DISABLED);
        mailboxSettings.setAutomaticRepliesSetting(automaticRepliesSetting);
        
        graphClient.users(userId)
            .mailboxSettings()
            .buildRequest()
            .patch(mailboxSettings);
    }
} 