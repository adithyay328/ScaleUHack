export default function Page({params}) : { params: { studentid: Number } }  {
  const studentid = params.studentid;

  return (
    <div className="w-full">
      <div className="w-1/5 h-screen bg-slate-500">
        <h1 className="italic">a</h1>
        <p className="italic">abcdefghi</p>
      </div>
    </div>
  );
};