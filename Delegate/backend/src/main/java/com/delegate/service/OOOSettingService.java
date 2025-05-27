package com.delegate.service;

import com.delegate.model.OOOSetting;
import com.delegate.repository.OOOSettingRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class OOOSettingService {
    private final OOOSettingRepository oooSettingRepository;
    private final AuditLogService auditLogService;

    @Transactional(readOnly = true)
    public List<OOOSetting> findByUserId(UUID userId) {
        return oooSettingRepository.findByUserId(userId);
    }

    @Transactional(readOnly = true)
    public List<OOOSetting> findActiveSettings(UUID userId, LocalDate date) {
        return oooSettingRepository.findByUserIdAndStartDateLessThanEqualAndEndDateGreaterThanEqual(
            userId, date, date);
    }

    @Transactional
    public OOOSetting createSetting(OOOSetting setting, UUID actorId) {
        validateDates(setting);
        OOOSetting savedSetting = oooSettingRepository.save(setting);
        auditLogService.logCreation("OOOSetting", savedSetting.getId(), actorId, savedSetting);
        return savedSetting;
    }

    @Transactional
    public OOOSetting updateSetting(UUID id, OOOSetting settingDetails, UUID actorId) {
        OOOSetting setting = oooSettingRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("OOO Setting not found"));
        
        validateDates(settingDetails);
        
        OOOSetting oldSetting = new OOOSetting();
        oldSetting.setStartDate(setting.getStartDate());
        oldSetting.setEndDate(setting.getEndDate());
        oldSetting.setMessage(setting.getMessage());
        oldSetting.setNotes(setting.getNotes());
        
        setting.setStartDate(settingDetails.getStartDate());
        setting.setEndDate(settingDetails.getEndDate());
        setting.setMessage(settingDetails.getMessage());
        setting.setNotes(settingDetails.getNotes());
        
        OOOSetting updatedSetting = oooSettingRepository.save(setting);
        auditLogService.logUpdate("OOOSetting", id, actorId, oldSetting, updatedSetting);
        return updatedSetting;
    }

    @Transactional
    public void deleteSetting(UUID id, UUID actorId) {
        OOOSetting setting = oooSettingRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("OOO Setting not found"));
        
        oooSettingRepository.deleteById(id);
        auditLogService.logDeletion("OOOSetting", id, actorId, setting);
    }

    private void validateDates(OOOSetting setting) {
        if (setting.getStartDate().isAfter(setting.getEndDate())) {
            throw new IllegalArgumentException("Start date must be before end date");
        }
    }
} 