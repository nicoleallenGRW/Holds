select l.code as "Location", ip.call_number_norm as "call number", b.best_title_norm as "Title", b.best_author_norm as  "Author",  max(ip.barcode) as "barcode"
from sierra_view.item_record i
join sierra_view.bib_record_item_record_link bi on bi.item_record_id=i.id
join sierra_view.item_record_property ip on ip.item_record_id=i.record_id
join sierra_view.location l on l.code=i.location_code
join sierra_view.location_name ln on ln.location_id=l.id and iii_language_id=1
join sierra_view.bib_record_property b on b.bib_record_id=bi.bib_record_id
join sierra_view.itype_property itp on itp.code_num=i.itype_code_num
join sierra_view.itype_property_name itpn on itpn.itype_property_id = itp.id and itpn.iii_language_id=1
join sierra_view.hold h on h.record_id=b.bib_record_id and h.status='0' and h.placed_gmt < (now() - interval '5 day') and h.is_frozen='f'
where i.item_status_code='-'
and i.id not in (select c.item_record_id from sierra_view.checkout c) and ip.call_number_norm not like '%express%'
group by h.record_id, h.is_frozen, b.bib_record_id,l.code, ln.name, ip.call_number_norm, b.best_author_norm, b.best_title_norm, itpn.name

order by l.code