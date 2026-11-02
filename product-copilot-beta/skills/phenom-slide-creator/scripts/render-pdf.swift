import PDFKit
import AppKit
let args = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: args[1]))!
let out = args[2]
for i in 0..<doc.pageCount {
  let p = doc.page(at: i)!
  let img = p.thumbnail(of: NSSize(width: 960, height: 540), for: .mediaBox)
  let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
  try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(out)/s\(String(format: "%02d", i+1)).png"))
}
print(doc.pageCount)
