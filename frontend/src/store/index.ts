/**
 * Global state management using Zustand
 */
import { create } from 'zustand'
import dayjs from 'dayjs'

interface DateRange {
  start_date: string;
  end_date: string;
}

interface FilterState {
  dateRange: DateRange;
  channels: string[];
  patternCategories: string[];
  regions: string[];
  setDateRange: (range: DateRange) => void;
  setChannels: (channels: string[]) => void;
  setPatternCategories: (categories: string[]) => void;
  setRegions: (regions: string[]) => void;
  resetFilters: () => void;
}

export const useFilterStore = create<FilterState>((set) => ({
  dateRange: {
    start_date: dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
    end_date: dayjs().format('YYYY-MM-DD'),
  },
  channels: [],
  patternCategories: [],
  regions: [],
  setDateRange: (range) => set({ dateRange: range }),
  setChannels: (channels) => set({ channels }),
  setPatternCategories: (categories) => set({ patternCategories: categories }),
  setRegions: (regions) => set({ regions }),
  resetFilters: () => set({
    dateRange: {
      start_date: dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
      end_date: dayjs().format('YYYY-MM-DD'),
    },
    channels: [],
    patternCategories: [],
    regions: [],
  }),
}))

interface UIState {
  loading: boolean;
  currentPage: string;
  setLoading: (loading: boolean) => void;
  setCurrentPage: (page: string) => void;
}

export const useUIStore = create<UIState>((set) => ({
  loading: false,
  currentPage: 'dashboard',
  setLoading: (loading) => set({ loading }),
  setCurrentPage: (page) => set({ currentPage: page }),
}))
