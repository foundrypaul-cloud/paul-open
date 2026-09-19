import { Capacitor } from '@capacitor/core';
import { Purchases } from '@revenuecat/purchases-capacitor';
import { RevenueCatUI } from '@revenuecat/purchases-capacitor-ui';
import type { SubscriptionState } from '../types';

const ENTITLEMENT =
  (import.meta.env.VITE_REVENUECAT_ENTITLEMENT_ID as string | undefined) || 'pro_access';

let configured = false;

function sdkKey(): string | undefined {
  const platform = Capacitor.getPlatform();
  if (platform === 'android') {
    return import.meta.env.VITE_REVENUECAT_ANDROID_API_KEY as string | undefined;
  }
  if (platform === 'ios') {
    return import.meta.env.VITE_REVENUECAT_IOS_API_KEY as string | undefined;
  }
  return undefined;
}

export async function refreshSubscription(): Promise<SubscriptionState> {
  const platform = Capacitor.getPlatform();
  if (!Capacitor.isNativePlatform()) {
    return {
      available: false,
      configured: false,
      isPro: false,
      platform,
      message: 'RevenueCat purchases run in the native Android/iOS build.',
    };
  }

  const apiKey = sdkKey();
  if (!apiKey) {
    return {
      available: true,
      configured: false,
      isPro: false,
      platform,
      message: 'RevenueCat SDK key is not configured for this build.',
    };
  }

  if (!configured) {
    await Purchases.configure({ apiKey });
    configured = true;
  }

  const { customerInfo } = await Purchases.getCustomerInfo();
  return {
    available: true,
    configured: true,
    isPro: Boolean(customerInfo.entitlements.active[ENTITLEMENT]),
    platform,
  };
}

export async function presentUpgrade(): Promise<SubscriptionState> {
  const initial = await refreshSubscription();
  if (!initial.available || !initial.configured) return initial;

  await RevenueCatUI.presentPaywallIfNeeded({
    requiredEntitlementIdentifier: ENTITLEMENT,
  });
  return refreshSubscription();
}

export async function restorePurchases(): Promise<SubscriptionState> {
  const initial = await refreshSubscription();
  if (!initial.available || !initial.configured) return initial;
  await Purchases.restorePurchases();
  return refreshSubscription();
}

export async function openCustomerCenter(): Promise<void> {
  const state = await refreshSubscription();
  if (!state.available || !state.configured) {
    throw new Error(state.message || 'RevenueCat is unavailable.');
  }
  await RevenueCatUI.presentCustomerCenter();
}
