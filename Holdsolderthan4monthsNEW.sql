SELECT 
phrase.index_entry AS "Call Number",
bib.record_num as "Bib No.",
prop.material_code as "Mat Type",
prop.best_title as "Title", 
prop.best_author as "Author", 
hold.placed_gmt as "Hold Placed",
hold.note as "Hold Note",
var.field_content "Pub date"
  

 from 

 Sierra_view.varfield_view as Var
 Join sierra_view.order_record as ord on ord.record_id = var.record_id
 Join sierra_view.bib_record_order_record_link as link on link.order_record_id = ord.record_id
 Join sierra_view.bib_view as bib on bib.id = link.bib_record_id
 join sierra_view.bib_record_property as prop on prop.bib_record_id = bib.id
 join sierra_view.phrase_entry as phrase on phrase.record_id = prop.bib_record_id
 left join sierra_view.hold as hold on hold.record_id = prop.bib_record_id


 where

 var.record_type_code = 'o' and var.varfield_type_code = 'n' 
   and hold.placed_gmt < (now() - interval '120 day')and hold.is_frozen='f' and phrase.index_tag = 'c'

   order by

phrase.index_entry,
prop.material_code,
prop.best_title;