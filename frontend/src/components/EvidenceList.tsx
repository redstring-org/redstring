type EvidenceListProps = {
  title: string;
  items: string[];
  emptyText: string;
};

export function EvidenceList({ title, items, emptyText }: EvidenceListProps) {
  return (
    <section className="panel">
      <div className="panel-eyebrow">{title}</div>
      {items.length === 0 ? (
        <p className="placeholder">{emptyText}</p>
      ) : (
        <ul className="evidence-list">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
