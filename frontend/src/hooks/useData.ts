/**
 * Custom hooks for data fetching using React Query
 */
import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'
import type {
  SalesTrendData, SalesRanking, SkuPerformance, PatternAnalysis,
  CustomerSegment, RfmAnalysis, LtvCacData, ChannelValue,
  LiveOverview, TrafficFunnel, CorrelationMatrix, ClusteringResult
} from '../services/types'

// Sales hooks
export function useSalesTrend(params: Record<string, any>) {
  return useQuery<{ data: SalesTrendData }>({
    queryKey: ['salesTrend', params],
    queryFn: () => api.getSalesTrend(params),
  })
}

export function useSalesRanking(params: Record<string, any>) {
  return useQuery<{ data: SalesRanking }>({
    queryKey: ['salesRanking', params],
    queryFn: () => api.getSalesRanking(params),
  })
}

// Product hooks
export function useProductPerformance(params: Record<string, any>) {
  return useQuery<{ data: SkuPerformance }>({
    queryKey: ['productPerformance', params],
    queryFn: () => api.getProductPerformance(params),
  })
}

export function useSkuRanking(params: Record<string, any>) {
  return useQuery<{ data: SalesRanking }>({
    queryKey: ['skuRanking', params],
    queryFn: () => api.getSkuRanking(params),
  })
}

export function usePatternAnalysis(params: Record<string, any>) {
  return useQuery<{ data: PatternAnalysis }>({
    queryKey: ['patternAnalysis', params],
    queryFn: () => api.getPatternAnalysis(params),
  })
}

export function useSkuInventory(params: Record<string, any>) {
  return useQuery({
    queryKey: ['skuInventory', params],
    queryFn: () => api.getSkuInventory(params),
  })
}

// Customer hooks
export function useCustomerSegments(params: Record<string, any>) {
  return useQuery<{ data: { segments: CustomerSegment[] } }>({
    queryKey: ['customerSegments', params],
    queryFn: () => api.getCustomerSegments(params),
  })
}

export function useCustomerRfm(params: Record<string, any>) {
  return useQuery<{ data: RfmAnalysis }>({
    queryKey: ['customerRfm', params],
    queryFn: () => api.getCustomerRfm(params),
  })
}

// Marketing hooks
export function useCampaigns(params: Record<string, any>) {
  return useQuery({
    queryKey: ['campaigns', params],
    queryFn: () => api.getCampaigns(params),
  })
}

export function useRoi(params: Record<string, any>) {
  return useQuery({
    queryKey: ['roi', params],
    queryFn: () => api.getRoi(params),
  })
}

// Live hooks
export function useLiveOverview(params: Record<string, any>) {
  return useQuery<{ data: LiveOverview }>({
    queryKey: ['liveOverview', params],
    queryFn: () => api.getLiveOverview(params),
  })
}

export function useLiveProducts(params: Record<string, any>) {
  return useQuery({
    queryKey: ['liveProducts', params],
    queryFn: () => api.getLiveProducts(params),
  })
}

// Traffic hooks
export function useTrafficChannels(params: Record<string, any>) {
  return useQuery({
    queryKey: ['trafficChannels', params],
    queryFn: () => api.getTrafficChannels(params),
  })
}

export function useTrafficFunnel(params: Record<string, any>) {
  return useQuery<{ data: TrafficFunnel }>({
    queryKey: ['trafficFunnel', params],
    queryFn: () => api.getTrafficFunnel(params),
  })
}

export function useLtvCac(params: Record<string, any>) {
  return useQuery<{ data: LtvCacData }>({
    queryKey: ['ltvCac', params],
    queryFn: () => api.getLtvCac(params),
  })
}

export function useChannelValue(params: Record<string, any>) {
  return useQuery<{ data: ChannelValue }>({
    queryKey: ['channelValue', params],
    queryFn: () => api.getChannelValue(params),
  })
}

// Advanced hooks
export function useCorrelation(params: Record<string, any>) {
  return useQuery<{ data: CorrelationMatrix }>({
    queryKey: ['correlation', params],
    queryFn: () => api.getCorrelation(params),
  })
}
