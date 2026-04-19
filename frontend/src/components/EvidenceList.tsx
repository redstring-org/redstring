type Props = {
  title: string;
  items: string[];
  emptyText: string;
  tone: "linked" | "weaken";
};

export function EvidenceList({ title, items, emptyText, tone }: Props) {
  return (
    <div>
      <p className="eyebrow">{title}</p>
      {items.length === 0 ? (
        <p className="placeholder">{emptyText}</p>
      ) : (
        <ul className="evidence-list">
          {items.map((item) => (
            <li key={item} className="ev-item">
              <span className={`ev-dot ev-dot-${tone}`} />
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
