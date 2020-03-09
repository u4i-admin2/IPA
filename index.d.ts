declare global {
    var $: any;
    var administered_by_stats: any;
    var angular: any;
    var d3: any;
    var UFIF: any;

    // Register type annotation for `ipa`
    var ipa: ipa.Ipa;

    // Register type annotation for `window.ipa`
    interface Window {
        ipa: ipa.Ipa;
    }

    namespace ipa {
        interface Ipa {
            colorsRange: Array<string>;
            commaCharacter: string | null,
            dLang: string;
            isMobile: boolean;
            lang: string;
            mediaPrefix: string;
            site: string;
            staticPrefix: string;
        }

        // ------------------------------------------
        // --- Prisons visualization (prisons.js) ---
        // ------------------------------------------

        interface CumulativeDictionary {
            [itemName: string]: number
        }

        interface AeaPrisonsMainData {
            [index: number]: AeaPrisonData;
            0: AeaPrisonsMainDataCumulatives;
        }

        interface IpaPrisonsMainData {
            [index: number]: IpaPrisonData;
            0: IpaPrisonsMainDataCumulatives;
        }

        interface MainDataCumulatives {
            total_prisoners_or_victims: number;
        }

        interface AeaPrisonsMainDataCumulatives extends MainDataCumulatives {
            humanrights_violations: CumulativeDictionary;
            procedural_violations: CumulativeDictionary;
            total_victims: number;
        }

        interface IpaPrisonsMainDataCumulatives extends MainDataCumulatives {
            activities: CumulativeDictionary;
            charges: CumulativeDictionary;
            ethnicities: CumulativeDictionary;
            genders: CumulativeDictionary;
            religions: CumulativeDictionary;
            total_prisoners: number;
            treatments: CumulativeDictionary;
        }

        interface PrisonData {
            administered_by: string | null;
            bio: string | null;
            i?: number
            id: string;
            latitude: number;
            longitude: number;
            name: number;
        }

        interface AeaPrisonData extends PrisonData {
            humanrights_violations: CumulativeDictionary;
            procedural_violations: CumulativeDictionary;
            total_victims: number;
        }

        interface IpaPrisonData extends PrisonData {
            activities: CumulativeDictionary;
            charges: CumulativeDictionary;
            ethnicities: CumulativeDictionary;
            genders: CumulativeDictionary;
            religions: CumulativeDictionary;
            total_prisoners: number;
            treatments: CumulativeDictionary;
        }

        // --------------------------------------------
        // --- Judges visualization (3tiles-vis.js) ---
        // --------------------------------------------

        abstract interface JudgeStats {
            prisoners_sentenced: number;
            total_executions: number;
            total_mistreatments: number;
        }

        interface JudgeStatsAea extends JudgeStats {
            total_amputation: number;
            total_flogging: number;
            total_reports: number;
            total_victims: number;
        }

        interface JudgeStatsIpa extends JudgeStats {
            average_months: number;
            average_years: number;
            total_lashes: number;
            total_months: number;
            total_verdicts: number;
            total_years: number;
        }

        abstract interface JudgeData {
            biography: string | null;
            forename: string | null;
            /** Image path, relative to MEDIA_ROOT (empty string if Judge has no image) */
            picture: string;
            picture_url: string | null;
            surname: string | null;
        }

        interface JudgeDataAea extends JudgeData {
            stats: JudgeStatsAea;
        }

        interface JudgeDataIpa extends JudgeData {
            stats: JudgeStatsIpa;
        }

        abstract interface JudgeTileData {
            geometry: {
                i?: number;
                x?: number;
                y?: number;
            };
            id: number;
        }

        interface JudgeTileDataAea extends JudgeTileData, JudgeDataAea {}
        interface JudgeTileDataIpa extends JudgeTileData, JudgeDataIpa {}

        type JudgesCircleVisMode = 'phone' | 'tablet-portrait' | 'tablet-landscape' | 'desktop-small' | 'desktop-large';

        namespace Judge {
            type BehaviourInstances = Array<number>;

            interface JudgeData {
                [fieldName: string]: any;
            }

            interface ChartEntityHoverInfo {
                [prisonerId: number]: {
                    forename: string,
                    surname: string,
                };
            }

            interface Scope {
                calcAge: (
                    (
                        year: number,
                        month: number,
                        day: number
                    ) => number | null
                );
                dLang: string;
                entityData: JudgeData;
                getJudgeSearch: (
                    (
                        judgeData: JudgeData,
                        lang: string
                    ) => string
                );
                lang: string;
                positionOrder: Array<string>;
                type: string;
                url: string;
                viewData: ViewDataAea | ViewDataIpa;
            }

            interface ViewData {
                behaviours: Array<BehaviourInstances>;
                judge: JudgeData;
            }

            interface ViewDataAea extends ViewData {
                total_amputations: number | null;
                total_executions: number | null;
                total_floggings: number | null;
                total_reports: number | null;
                total_victims: number | null;
            }

            interface ViewDataIpa extends ViewData {
                average_sentence: number;
                latest_sentence_prisoner_id: number;
                chart_entity_hover_info: ChartEntityHoverInfo;
                sentence: string;
                sentence_id: number;
                total_sentences: number;
                total_time_sentenced: number;
            }
        }

        interface InformationOverlayTriggerButtonClickedEvent extends CustomEvent {
            detail: {
                informationOverlaySlug: string;
            };
        }
    }
}

export {}
