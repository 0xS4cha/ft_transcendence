export interface FilterType {
    queue: string;
    server: string;
    ranked: string;   
}

export interface exportRef {
    export?: () => void;
    exportJson: () => void;
    exportXml: () => void;
}
