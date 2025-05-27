package com.delegate.repository;

import com.delegate.model.Delegation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Repository
public interface DelegationRepository extends JpaRepository<Delegation, UUID> {
    List<Delegation> findByUserId(UUID userId);
    List<Delegation> findByDelegateUserId(UUID delegateUserId);
    List<Delegation> findByUserIdAndStartDateLessThanEqualAndEndDateGreaterThanEqual(
        UUID userId, LocalDate date, LocalDate date2);
    List<Delegation> findByDelegateUserIdAndStartDateLessThanEqualAndEndDateGreaterThanEqual(
        UUID delegateUserId, LocalDate date, LocalDate date2);
    List<Delegation> findByUserIdAndApplicationIdAndTaskType(
        UUID userId, UUID applicationId, String taskType);
} 