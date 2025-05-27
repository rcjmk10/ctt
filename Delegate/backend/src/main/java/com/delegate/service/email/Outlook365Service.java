package com.delegate.service.email;

import com.delegate.model.OOOSetting;
import com.delegate.model.Delegation;
import com.microsoft.graph.models.*;
import com.microsoft.graph.requests.GraphServiceClient;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.ArrayList;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;

@Service
public class Outlook365Service implements EmailProviderService {
    private static final Logger logger = LoggerFactory.getLogger(Outlook365Service.class);
    private final GraphServiceClient graphClient;

    public Outlook365Service(GraphServiceClient graphClient) {
        this.graphClient = graphClient;
    }

    @Override
    public void setOOOSetting(String userId, OOOSetting setting) {
        try {
            MailboxSettings mailboxSettings = new MailboxSettings();
            AutomaticRepliesMailTips automaticReplies = new AutomaticRepliesMailTips();
            automaticReplies.status = AutomaticRepliesMailTipsStatus.SCHEDULED;
            
            DateTimeTimeZone startTime = new DateTimeTimeZone();
            startTime.dateTime = setting.getStartDate().toString();
            startTime.timeZone = "UTC";
            
            DateTimeTimeZone endTime = new DateTimeTimeZone();
            endTime.dateTime = setting.getEndDate().toString();
            endTime.timeZone = "UTC";
            
            automaticReplies.scheduledStartDateTime = startTime;
            automaticReplies.scheduledEndDateTime = endTime;
            automaticReplies.internalReplyMessage = setting.getMessage();
            automaticReplies.externalReplyMessage = setting.getMessage();
            
            mailboxSettings.automaticRepliesSetting = automaticReplies;
            
            graphClient.users(userId)
                    .mailboxSettings()
                    .buildRequest()
                    .patch(mailboxSettings);
        } catch (Exception e) {
            logger.error("Failed to set OOO setting in Outlook 365", e);
            throw new RuntimeException("Failed to set OOO setting in Outlook 365", e);
        }
    }

    @Override
    public void clearOOOSetting(String userId) {
        try {
            MailboxSettings mailboxSettings = new MailboxSettings();
            AutomaticRepliesMailTips automaticReplies = new AutomaticRepliesMailTips();
            automaticReplies.status = AutomaticRepliesMailTipsStatus.DISABLED;
            mailboxSettings.automaticRepliesSetting = automaticReplies;
            
            graphClient.users(userId)
                    .mailboxSettings()
                    .buildRequest()
                    .patch(mailboxSettings);
        } catch (Exception e) {
            logger.error("Failed to clear OOO setting in Outlook 365", e);
            throw new RuntimeException("Failed to clear OOO setting in Outlook 365", e);
        }
    }

    @Override
    public OOOSetting getOOOSetting(String userId) {
        try {
            MailboxSettings mailboxSettings = graphClient.users(userId)
                    .mailboxSettings()
                    .buildRequest()
                    .get();

            if (mailboxSettings.automaticRepliesSetting.status == AutomaticRepliesMailTipsStatus.DISABLED) {
                return null;
            }

            OOOSetting setting = new OOOSetting();
            setting.setId("outlook-" + userId);
            setting.setUserId(userId);
            setting.setStartDate(OffsetDateTime.parse(mailboxSettings.automaticRepliesSetting.scheduledStartDateTime.dateTime));
            setting.setEndDate(OffsetDateTime.parse(mailboxSettings.automaticRepliesSetting.scheduledEndDateTime.dateTime));
            setting.setMessage(mailboxSettings.automaticRepliesSetting.internalReplyMessage);
            setting.setStatus("active");
            setting.setCreatedAt(OffsetDateTime.now(ZoneOffset.UTC));
            setting.setUpdatedAt(OffsetDateTime.now(ZoneOffset.UTC));
            
            return setting;
        } catch (Exception e) {
            logger.error("Failed to get OOO setting from Outlook 365", e);
            throw new RuntimeException("Failed to get OOO setting from Outlook 365", e);
        }
    }

    @Override
    public void createDelegation(Delegation delegation) {
        try {
            // First, set up the delegation
            DelegateMailboxSettings delegateSettings = new DelegateMailboxSettings();
            delegateSettings.emailAddress = new EmailAddress();
            delegateSettings.emailAddress.address = delegation.getDelegateId();
            delegateSettings.permissions = delegation.getPermissions().toArray(new String[0]);

            graphClient.users(delegation.getDelegatorId())
                    .mailboxSettings()
                    .delegates()
                    .buildRequest()
                    .post(delegateSettings);

            // If there's an active OOO setting, apply it
            OOOSetting oooSetting = getOOOSetting(delegation.getDelegatorId());
            if (oooSetting != null && "active".equals(oooSetting.getStatus())) {
                setOOOSetting(delegation.getDelegatorId(), oooSetting);
            }
        } catch (Exception e) {
            logger.error("Failed to create delegation in Outlook 365", e);
            throw new RuntimeException("Failed to create delegation in Outlook 365", e);
        }
    }

    @Override
    public void removeDelegation(Delegation delegation) {
        try {
            graphClient.users(delegation.getDelegatorId())
                    .mailboxSettings()
                    .delegates(delegation.getDelegateId())
                    .buildRequest()
                    .delete();
        } catch (Exception e) {
            logger.error("Failed to remove delegation in Outlook 365", e);
            throw new RuntimeException("Failed to remove delegation in Outlook 365", e);
        }
    }

    @Override
    public void updateDelegation(Delegation delegation) {
        try {
            DelegateMailboxSettings delegateSettings = new DelegateMailboxSettings();
            delegateSettings.permissions = delegation.getPermissions().toArray(new String[0]);

            graphClient.users(delegation.getDelegatorId())
                    .mailboxSettings()
                    .delegates(delegation.getDelegateId())
                    .buildRequest()
                    .patch(delegateSettings);
        } catch (Exception e) {
            logger.error("Failed to update delegation in Outlook 365", e);
            throw new RuntimeException("Failed to update delegation in Outlook 365", e);
        }
    }

    @Override
    public List<Delegation> getDelegations(String userId) {
        try {
            List<DelegateMailboxSettings> delegates = graphClient.users(userId)
                    .mailboxSettings()
                    .delegates()
                    .buildRequest()
                    .get();

            List<Delegation> result = new ArrayList<>();
            for (DelegateMailboxSettings delegate : delegates) {
                Delegation delegation = new Delegation();
                delegation.setId("outlook-" + userId + "-" + delegate.emailAddress.address);
                delegation.setDelegatorId(userId);
                delegation.setDelegateId(delegate.emailAddress.address);
                delegation.setStartDate(OffsetDateTime.now(ZoneOffset.UTC));
                delegation.setEndDate(OffsetDateTime.now(ZoneOffset.UTC).plusYears(1));
                delegation.setStatus("active");
                delegation.setPermissions(List.of(delegate.permissions));
                delegation.setCreatedAt(OffsetDateTime.now(ZoneOffset.UTC));
                delegation.setUpdatedAt(OffsetDateTime.now(ZoneOffset.UTC));
                result.add(delegation);
            }
            return result;
        } catch (Exception e) {
            logger.error("Failed to get delegations from Outlook 365", e);
            throw new RuntimeException("Failed to get delegations from Outlook 365", e);
        }
    }
} 