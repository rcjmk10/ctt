import { Client } from '@microsoft/microsoft-graph-client';
import type { EmailProviderService } from './EmailProviderService';
import type { OOOSetting } from '../../types/oooSetting';
import type { Delegation } from '../../types/delegation';
import { logger } from '../../utils/logger';

export class Outlook365Service implements EmailProviderService {
  private client: Client;

  constructor(accessToken: string) {
    this.client = Client.init({
      authProvider: (done) => {
        done(null, accessToken);
      },
    });
  }

  async setOOOSetting(userId: string, setting: OOOSetting): Promise<void> {
    try {
      await this.client
        .api(`/users/${userId}/mailboxSettings`)
        .patch({
          automaticRepliesSetting: {
            status: 'scheduled',
            scheduledStartDateTime: {
              dateTime: setting.startDate,
              timeZone: 'UTC',
            },
            scheduledEndDateTime: {
              dateTime: setting.endDate,
              timeZone: 'UTC',
            },
            internalReplyMessage: setting.message,
            externalReplyMessage: setting.message,
          },
        });
    } catch (error) {
      logger.error('Failed to set OOO setting in Outlook 365:', error);
      throw new Error('Failed to set OOO setting in Outlook 365');
    }
  }

  async clearOOOSetting(userId: string): Promise<void> {
    try {
      await this.client
        .api(`/users/${userId}/mailboxSettings`)
        .patch({
          automaticRepliesSetting: {
            status: 'disabled',
          },
        });
    } catch (error) {
      logger.error('Failed to clear OOO setting in Outlook 365:', error);
      throw new Error('Failed to clear OOO setting in Outlook 365');
    }
  }

  async getOOOSetting(userId: string): Promise<OOOSetting | null> {
    try {
      const response = await this.client
        .api(`/users/${userId}/mailboxSettings`)
        .get();

      const setting = response.automaticRepliesSetting;
      if (setting.status === 'disabled') {
        return null;
      }

      return {
        id: 'outlook-' + userId,
        userId,
        startDate: setting.scheduledStartDateTime.dateTime,
        endDate: setting.scheduledEndDateTime.dateTime,
        message: setting.internalReplyMessage,
        status: 'active',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
    } catch (error) {
      logger.error('Failed to get OOO setting from Outlook 365:', error);
      throw new Error('Failed to get OOO setting from Outlook 365');
    }
  }

  async createDelegation(delegation: Delegation): Promise<void> {
    try {
      // First, set up the delegation
      await this.client
        .api(`/users/${delegation.delegatorId}/mailboxSettings/delegates`)
        .post({
          emailAddress: {
            address: delegation.delegateId,
          },
          permissions: delegation.permissions,
        });

      // If there's an active OOO setting, apply it
      const oooSetting = await this.getOOOSetting(delegation.delegatorId);
      if (oooSetting && oooSetting.status === 'active') {
        await this.setOOOSetting(delegation.delegatorId, oooSetting);
      }
    } catch (error) {
      logger.error('Failed to create delegation in Outlook 365:', error);
      throw new Error('Failed to create delegation in Outlook 365');
    }
  }

  async removeDelegation(delegation: Delegation): Promise<void> {
    try {
      await this.client
        .api(`/users/${delegation.delegatorId}/mailboxSettings/delegates/${delegation.delegateId}`)
        .delete();
    } catch (error) {
      logger.error('Failed to remove delegation in Outlook 365:', error);
      throw new Error('Failed to remove delegation in Outlook 365');
    }
  }

  async updateDelegation(delegation: Delegation): Promise<void> {
    try {
      await this.client
        .api(`/users/${delegation.delegatorId}/mailboxSettings/delegates/${delegation.delegateId}`)
        .patch({
          permissions: delegation.permissions,
        });
    } catch (error) {
      logger.error('Failed to update delegation in Outlook 365:', error);
      throw new Error('Failed to update delegation in Outlook 365');
    }
  }

  async getDelegations(userId: string): Promise<Delegation[]> {
    try {
      const response = await this.client
        .api(`/users/${userId}/mailboxSettings/delegates`)
        .get();

      return response.value.map((delegate: any) => ({
        id: `outlook-${userId}-${delegate.emailAddress.address}`,
        delegatorId: userId,
        delegateId: delegate.emailAddress.address,
        startDate: new Date().toISOString(),
        endDate: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(), // 1 year from now
        status: 'active',
        permissions: delegate.permissions,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      }));
    } catch (error) {
      logger.error('Failed to get delegations from Outlook 365:', error);
      throw new Error('Failed to get delegations from Outlook 365');
    }
  }
} 