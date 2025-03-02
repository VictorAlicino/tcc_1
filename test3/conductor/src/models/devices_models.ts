interface HVACMode {
    cool: "Cool";
    heat: "Heat";
    dry: "Dry";
    fan: "Fan";
    auto: "Auto";
}

export interface HVACPayload {
    power_state: string;
    vendor: string | null;
    model: string | null;
    mode: string
    fan_speed: string;
    swing_vertical: string | null;
    swing_horizontal: string | null;
    is_celsius: boolean | null;
    temperature: number;
    quiet: boolean | null;
    turbo: boolean | null;
    economy: boolean | null;
    light: boolean | null;
    filter: boolean | null;
    clean: boolean | null;
    beep: boolean | null;
    sleep: boolean | null;
    state_mode: string | null;
}