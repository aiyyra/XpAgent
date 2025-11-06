// This button will be wrapped in the logo and app name.
// This button will create a new chat on a new thread

// Thread management will come later
import * as motion from "motion/react-client";

export default function LogoButton() {
  return (
    <motion.button
      className="flex cursor-pointer items-center gap-2"
      //   onClick={() => setThreadId(null)}
      onClick={undefined} // set only click to create new chat by creating new thread and render
      animate={{
        // marginLeft: !chatHistoryOpen ? 48 : 0,
        // retrieve chatHistoryOpen from context later
        marginLeft: 0,
      }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 30,
      }}
    >
      {/* <AppLogo /> add AppLogo by uploading logo to public and importing it */}
      <span className="text-xl font-semibold tracking-tight">XpAgent</span>
    </motion.button>
  );
}
