package com.delegate.repository;

import com.delegate.model.OOOSetting;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Repository
public interface OOOSettingRepository extends JpaRepository<OOOSetting, UUID> {
    List<OOOSetting> findByUserId(UUID userId);
    List<OOOSetting> findByUserIdAndStartDateLessThanEqualAndEndDateGreaterThanEqual(
        UUID userId, LocalDate date, LocalDate date2);
    List<OOOSetting> findByApplicationIdAndStartDateLessThanEqualAndEndDateGreaterThanEqual(
        UUID applicationId, LocalDate date, LocalDate date2);
} 